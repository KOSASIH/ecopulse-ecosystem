pragma solidity ^0.8.0;

import "https://github.com/OpenZeppelin/openzeppelin-solidity/contracts/token/ERC20/SafeERC20.sol";
import "https://github.com/OpenZeppelin/openzeppelin-solidity/contracts/math/SafeMath.sol";

contract EcoPulseToken {
    // Token details
    string public name = "EcoPulse Token";
    string public symbol = "EP";
    uint8 public decimals = 18;
    uint256 public totalSupply = 10_000_000_000 * (10 ** decimals);

    // Mapping of balances
    mapping (address => uint256) public balances;

    // Mapping of allowances
    mapping (address => mapping (address => uint256)) public allowances;

    // Event emitted when tokens are transferred
    event Transfer(address indexed from, address indexed to, uint256 value);

    // Event emitted when approval is given
    event Approval(address indexed owner, address indexed spender, uint256 value);

    // Constructor
    constructor() public {
        // Initialize token balances
        balances[msg.sender] = totalSupply;
    }

    // Transfer tokens
    function transfer(address to, uint256 value) public returns (bool) {
        require(balances[msg.sender] >= value, "Insufficient balance");
        balances[msg.sender] -= value;
        balances[to] += value;
        emit Transfer(msg.sender, to, value);
        return true;
    }

    // Approve tokens for spending
    function approve(address spender, uint256 value) public returns (bool) {
        allowances[msg.sender][spender] = value;
        emit Approval(msg.sender, spender, value);
        return true;
    }

    // Transfer tokens from one address to another
    function transferFrom(address from, address to, uint256 value) public returns (bool) {
        require(allowances[from][msg.sender] >= value, "Insufficient allowance");
        require(balances[from] >= value, "Insufficient balance");
        balances[from] -= value;
        balances[to] += value;
        allowances[from][msg.sender] -= value;
        emit Transfer(from, to, value);
        return true;
    }

    // Get token balance
    function balanceOf(address owner) public view returns (uint256) {
        return balances[owner];
    }

    // Get token allowance
    function allowance(address owner, address spender) public view returns (uint256) {
        return allowances[owner][spender];
    }
}
