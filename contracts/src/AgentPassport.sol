// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract AgentPassport {
    mapping(address => string) public identities;
    mapping(address => uint256) public reputation;
    uint256 public totalAgents;

    event AgentRegistered(address indexed agent, string name, uint256 timestamp);

    function register(string calldata _name) external {
        require(bytes(identities[msg.sender]).length == 0, "Already registered");
        identities[msg.sender] = _name;
        reputation[msg.sender] = 100;
        totalAgents++;
        emit AgentRegistered(msg.sender, _name, block.timestamp);
    }

    function agentCount() external view returns (uint256) {
        return totalAgents;
    }
}
