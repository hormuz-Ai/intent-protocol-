// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract EscrowSettlement {
    address public treasury;
    uint256 public constant PROTOCOL_FEE_BPS = 10;
    uint256 public constant BPS_DENOMINATOR = 10000;

    enum Status { Pending, Fulfilled, Slashed, Refunded }

    struct Escrow {
        address user;
        address solver;
        uint256 totalAmount;
        uint256 lockedAmount;
        uint256 feeAmount;
        uint256 deadline;
        Status status;
        bytes32 proofHash;
    }

    mapping(bytes32 => Escrow) public escrows;
    event Deposited(bytes32 indexed intentId, address user, address solver, uint256 total, uint256 fee);
    event Fulfilled(bytes32 indexed intentId, bytes32 proofHash);
    event Slashed(bytes32 indexed intentId, address solver);
    event Refunded(bytes32 indexed intentId, address user);

    constructor(address _treasury) {
        treasury = _treasury;
    }

    function deposit(bytes32 intentId, address solver, uint256 deadline) external payable {
        require(msg.value > 0, "No value");
        require(escrows[intentId].totalAmount == 0, "Intent exists");
        uint256 fee = (msg.value * PROTOCOL_FEE_BPS) / BPS_DENOMINATOR;
        uint256 locked = msg.value - fee;
        (bool sent, ) = treasury.call{value: fee}("");
        require(sent, "Fee transfer failed");
        escrows[intentId] = Escrow({
            user: msg.sender,
            solver: solver,
            totalAmount: msg.value,
            lockedAmount: locked,
            feeAmount: fee,
            deadline: deadline,
            status: Status.Pending,
            proofHash: bytes32(0)
        });
        emit Deposited(intentId, msg.sender, solver, msg.value, fee);
    }

    function verifyProof(bytes32 intentId, bytes32 proofHash) external {
        Escrow storage e = escrows[intentId];
        require(e.status == Status.Pending, "Not pending");
        require(block.timestamp <= e.deadline, "Expired");
        e.status = Status.Fulfilled;
        e.proofHash = proofHash;
        (bool sent, ) = e.solver.call{value: e.lockedAmount}("");
        require(sent, "Solver pay failed");
        emit Fulfilled(intentId, proofHash);
    }

    function slash(bytes32 intentId) external {
        Escrow storage e = escrows[intentId];
        require(e.status == Status.Pending, "Not pending");
        require(block.timestamp > e.deadline, "Not expired");
        e.status = Status.Slashed;
        (bool sent, ) = e.user.call{value: e.lockedAmount}("");
        require(sent, "Refund failed");
        emit Slashed(intentId, e.solver);
    }

    function refund(bytes32 intentId) external {
        Escrow storage e = escrows[intentId];
        require(e.status == Status.Pending, "Not pending");
        e.status = Status.Refunded;
        (bool sent, ) = e.user.call{value: e.lockedAmount}("");
        require(sent, "Refund failed");
        emit Refunded(intentId, e.user);
    }
}
