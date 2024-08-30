pragma solidity ^0.8.0;

import "https://github.com/OpenZeppelin/openzeppelin-solidity/contracts/token/ERC721/SafeERC721.sol";
import "https://github.com/OpenZeppelin/openzeppelin-solidity/contracts/math/SafeMath.sol";

contract EcoPulseNFT {
    // NFT details
    string public name = "EcoPulse NFT";
    string public symbol = "EPNFT";

    // Mapping of NFTs
    mapping (uint256 => address) public nftOwners;

    // Mapping of NFT metadata
    mapping (uint256 => string) public nftMetadata;

    // Event emitted when NFT is minted
    event Mint(address indexed owner, uint256 indexed tokenId, string metadata);

    // Event emitted when NFT is transferred
    event Transfer(address indexed from, address indexed to, uint256 indexed tokenId);

    // Event emitted when NFT is burned
    event Burn(address indexed owner, uint256 indexed tokenId);

    // Constructor
    constructor() public {
        // Initialize NFT counter
        uint256 public nftCounter = 0;
    }

    // Mint a new NFT
    function mint(address to, string memory metadata) public returns (uint256) {
        require(to != address(0), "Invalid recipient");
        uint256 tokenId = nftCounter++;
        nftOwners[tokenId] = to;
        nftMetadata[tokenId] = metadata;
        emit Mint(to, tokenId, metadata);
        return tokenId;
    }

    // Transfer NFT
    function transfer(address to, uint256 tokenId) public returns (bool) {
        require(nftOwners[tokenId] == msg.sender, "Only the owner can transfer");
        require(to != address(0), "Invalid recipient");
        nftOwners[tokenId] = to;
        emit Transfer(msg.sender, to, tokenId);
        return true;
    }

    // Burn NFT
    function burn(uint256 tokenId) public returns (bool) {
        require(nftOwners[tokenId] == msg.sender, "Only the owner can burn");
        delete nftOwners[tokenId];
        delete nftMetadata[tokenId];
        emit Burn(msg.sender, tokenId);
        return true;
    }

    // Get NFT owner
    function ownerOf(uint256 tokenId) public view returns (address) {
        return nftOwners[tokenId];
    }

    // Get NFT metadata
    function getMetadata(uint256 tokenId) public view returns (string memory) {
        return nftMetadata[tokenId];
    }

    // Get NFT count
    function getNFTCount() public view returns (uint256) {
        return nftCounter;
    }
}
