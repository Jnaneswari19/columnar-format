// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract MyToken {
    // --- Step 2: Token metadata ---
    string public name;
    string public symbol;
    uint8 public decimals;
    uint256 public totalSupply;

    // --- Step 2: Balances and allowances ---
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;

    // --- Step 3: Events ---
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);

    // --- Step 2: Constructor ---
    constructor(
        string memory _name,
        string memory _symbol,
        uint8 _decimals,
        uint256 _initialSupply
    ) {
        name = _name;
        symbol = _symbol;
        decimals = _decimals;

        uint256 scaledSupply = _initialSupply * (10 ** uint256(_decimals));
        totalSupply = scaledSupply;
        balanceOf[msg.sender] = scaledSupply;

        emit Transfer(address(0), msg.sender, scaledSupply);
    }

    // --- Step 4: Transfer function ---
    function transfer(address _to, uint256 _value) public returns (bool success) {
        require(_to != address(0), "Cannot transfer to zero address");
        require(balanceOf[msg.sender] >= _value, "Insufficient balance");

        balanceOf[msg.sender] -= _value;
        balanceOf[_to] += _value;

        emit Transfer(msg.sender, _to, _value);
        return true;
    }

    // --- Step 5: Approve function ---
    function approve(address _spender, uint256 _value) public returns (bool success) {
        require(_spender != address(0), "Cannot approve zero address");

        allowance[msg.sender][_spender] = _value;

        emit Approval(msg.sender, _spender, _value);
        return true;
    }

    // --- Step 6: TransferFrom function ---
    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success) {
        require(_to != address(0), "Cannot transfer to zero address");
        require(balanceOf[_from] >= _value, "Insufficient balance");
        require(allowance[_from][msg.sender] >= _value, "Allowance exceeded");

        balanceOf[_from] -= _value;
        balanceOf[_to] += _value;
        allowance[_from][msg.sender] -= _value;

        emit Transfer(_from, _to, _value);
        return true;
    }

    // --- Step 7: Helper function to get total supply ---
    function getTotalSupply() public view returns (uint256) {
        return totalSupply;
    }

    // --- Step 7: Helper function to get token info ---
    function getTokenInfo() public view returns (string memory, string memory, uint8, uint256) {
        return (name, symbol, decimals, totalSupply);
    }
}
