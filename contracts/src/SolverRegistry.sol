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

    event SolverRegistered(address indexed solver, string endpoint);
    event SolverUpdated(address indexed solver, uint256 reputation, bool active);

    function register(string memory _endpoint, string[] memory _capabilities) public {
        require(!solvers[msg.sender].active, "Already registered");
        solvers[msg.sender] = Solver(_endpoint, _capabilities, 100, true);
        solverAddresses.push(msg.sender);
        emit SolverRegistered(msg.sender, _endpoint);
    }

    function updateReputation(address _solver, uint256 _newReputation) external {
        solvers[_solver].reputation = _newReputation;
        emit SolverUpdated(_solver, _newReputation, solvers[_solver].active);
    }

    function setActive(address _solver, bool _active) external {
        solvers[_solver].active = _active;
        emit SolverUpdated(_solver, solvers[_solver].reputation, _active);
    }

    function getSolver(address _solver) public view returns (Solver memory) {
        return solvers[_solver];
    }

    function getAllActiveSolvers() public view returns (address[] memory, Solver[] memory) {
        uint256 activeCount = 0;
        for (uint i = 0; i < solverAddresses.length; i++) {
            if (solvers[solverAddresses[i]].active) activeCount++;
        }
        address[] memory activeAddresses = new address[](activeCount);
        Solver[] memory activeSolvers = new Solver[](activeCount);
        uint256 index = 0;
        for (uint i = 0; i < solverAddresses.length; i++) {
            if (solvers[solverAddresses[i]].active) {
                activeAddresses[index] = solverAddresses[i];
                activeSolvers[index] = solvers[solverAddresses[i]];
                index++;
            }
        }
        return (activeAddresses, activeSolvers);
    }
}
