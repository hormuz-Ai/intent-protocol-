// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract AgentReferral {
    mapping(address => address) public referrerOf;
    mapping(address => uint256) public totalEarned;
    uint256 public constant REFERRAL_SHARE = 1000; // 10%

    event AgentReferred(address indexed agent, address indexed referrer, uint256 timestamp);

    function registerWithReferral(string calldata _name, address _referrer) external {
        require(referrerOf[msg.sender] == address(0), "Already registered");
        referrerOf[msg.sender] = _referrer;
        emit AgentReferred(msg.sender, _referrer, block.timestamp);
    }

    function distributeReward(address _agent, uint256 _feeAmount) external {
        address ref = referrerOf[_agent];
        if (ref != address(0)) {
            uint256 reward = (_feeAmount * REFERRAL_SHARE) / 10000;
            totalEarned[ref] += reward;
            payable(ref).transfer(reward);
        }
    }
}
