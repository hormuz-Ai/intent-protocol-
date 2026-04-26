// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract INTPToken is ERC20, Ownable {
    uint256 public constant MAX_SUPPLY = 1_000_000_000 * 10**18;
    address public treasury;

    constructor(address _treasury) ERC20("Intent Protocol", "INTP") Ownable(msg.sender) {
        treasury = _treasury;
        _mint(treasury, MAX_SUPPLY);
    }
}
