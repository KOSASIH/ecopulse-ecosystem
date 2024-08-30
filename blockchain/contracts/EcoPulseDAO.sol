pragma solidity ^0.8.0;

import "https://github.com/OpenZeppelin/openzeppelin-solidity/contracts/math/SafeMath.sol";
import "https://github.com/OpenZeppelin/openzeppelin-solidity/contracts/utils/Address.sol";

contract EcoPulseDAO {
    // DAO details
    string public name = "EcoPulse DAO";
    string public symbol = "EPDAO";

    // Mapping of proposals
    mapping (uint256 => Proposal) public proposals;

    // Mapping of votes
    mapping (address => mapping (uint256 => bool)) public votes;

    // Event emitted when a new proposal is created
    event NewProposal(uint256 indexed proposalId, address indexed proposer, string description);

    // Event emitted when a proposal is voted on
    event Vote(uint256 indexed proposalId, address indexed voter, bool vote);

    // Event emitted when a proposal is executed
    event ExecuteProposal(uint256 indexed proposalId, address indexed executor);

    // Event emitted when a proposal is cancelled
    event CancelProposal(uint256 indexed proposalId, address indexed canceller);

    // Proposal struct
    struct Proposal {
        uint256 id;
        address proposer;
        string description;
        uint256 yesVotes;
        uint256 noVotes;
        bool executed;
    }

    // Proposal counter
    uint256 public proposalCounter = 0;

    // Constructor
    constructor() public {
        // Initialize DAO treasury
        treasury = address(this);
    }

    // Create a new proposal
    function newProposal(string memory description) public returns (uint256) {
        require(msg.sender != address(0), "Invalid proposer");
        uint256 proposalId = proposalCounter++;
        proposals[proposalId] = Proposal(proposalId, msg.sender, description, 0, 0, false);
        emit NewProposal(proposalId, msg.sender, description);
        return proposalId;
    }

    // Vote on a proposal
    function vote(uint256 proposalId, bool vote) public {
        require(proposals[proposalId].proposer != address(0), "Invalid proposal");
        require(!votes[msg.sender][proposalId], "Already voted");
        if (vote) {
            proposals[proposalId].yesVotes++;
        } else {
            proposals[proposalId].noVotes++;
        }
        votes[msg.sender][proposalId] = true;
        emit Vote(proposalId, msg.sender, vote);
    }

    // Execute a proposal
    function executeProposal(uint256 proposalId) public {
        require(proposals[proposalId].proposer != address(0), "Invalid proposal");
        require(!proposals[proposalId].executed, "Already executed");
        require(proposals[proposalId].yesVotes > proposals[proposalId].noVotes, "Proposal not approved");
        // Execute the proposal logic here
        proposals[proposalId].executed = true;
        emit ExecuteProposal(proposalId, msg.sender);
    }

    // Cancel a proposal
    function cancelProposal(uint256 proposalId) public {
        require(proposals[proposalId].proposer != address(0), "Invalid proposal");
        require(!proposals[proposalId].executed, "Already executed");
        delete proposals[proposalId];
        emit CancelProposal(proposalId, msg.sender);
    }

    // Get proposal details
    function getProposal(uint256 proposalId) public view returns (Proposal memory) {
        return proposals[proposalId];
    }

    // Get vote details
    function getVote(uint256 proposalId, address voter) public view returns (bool) {
        return votes[voter][proposalId];
    }
}
