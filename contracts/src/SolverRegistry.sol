// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract SolverRegistry {
    struct Solver {
        string endpoint;
        string[] capabilities;
        uint256 reputation;
        bool active;
    }
    mapping(address => Solver) public solvers;
    address[] public solverAddresses;

    function register(string memory _endpoint, string[] memory _capabilities) public {
        solvers[msg.sender] = Solver(_endpoint, _capabilities, 100, true);
        solverAddresses.push(msg.sender);
    }

    function getAllActiveSolvers() public view returns (address[] memory, Solver[] memory) {
        uint256 activeCount = 0;
        for (uint i = 0; i < solverAddresses.length; i++) {
            if (solvers[solverAddresses[i]].active) activeCount++;
        }
        address[] memory activeAddrs = new address[](activeCount);
        Solver[] memory activeSolvers = new Solver[](activeCount);
        uint256 idx = 0;
        for (uint i = 0; i < solverAddresses.length; i++) {
            if (solvers[solverAddresses[i]].active) {
                activeAddrs[idx] = solverAddresses[i];
                activeSolvers[idx] = solvers[solverAddresses[i]];
                idx++;
            }
        }
        return (activeAddrs, activeSolvers);
    }
}
