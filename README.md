Columnar Format + ERC‑20 Token Project
This project demonstrates two parallel tracks:

🧠 Part A: Columnar Format Pipeline — a custom binary format (.ccol) for efficient data storage and retrieval using Python.
💰 Part B: ERC‑20 Token Contract — a Solidity-based token deployed and tested in Remix IDE.

📁 Project Structure
columnar-format/
├── contracts/
│   └── MyToken.sol              # ERC‑20 contract (Solidity)
│
├── data/
│   ├── sample.ccol              # Custom columnar format file
│   └── sample.csv               # Source CSV data
│
├── screenshots/
│   └── step8/
│       └── transfer-confirmation.png   # Proof of ERC‑20 transfer test
│
├── src/
│   ├── cli.py                   # CLI for CCOL pipeline
│   ├── reader.py                # CCOL reader
│   ├── writer.py                # CCOL writer
│   ├── types.py                 # Schema/type definitions
│   └── __pycache__/             # Auto‑generated Python cache
│
├── tests/
│   ├── roundtrip_test.py        # Round‑trip validation
│   ├── selective_read_bench.py  # Selective read benchmark
│   └── string_offsets_check.py  # String offset validation
│
├── LICENSE                      # License file
├── README.md                    # Documentation (Steps 1–8 complete)
└── SPEC.md                      # Specification notes

🧠 Part A: Columnar Format Pipeline
✅ Step 1–7 Summary
Implemented a custom binary format .ccol with:
. Header: b'CCOL1\x00\x00'
. Version: b'\x01\x00'
. Wrote writer.py to convert CSV → CCOL.
. Wrote reader.py to parse schema and rows.
. Verified round-trip conversion and column selection:
['id', 'price', 'name']
[1, 9.99, 'Alice']
[2, 15.5, 'Bob']
['Alice', 'Bob']

💰 Part B: ERC‑20 Token Contract
✅ Step 8: ERC‑20 Transfer Function Test
Deployed ERC‑20 contract in Remix IDE with:
. Name: MyToken
. Symbol: MKT
. Decimals: 18
. Initial Supply: 1000000000000000000 (1 token)
Called transfer() to send 1 token from Account[0] → Account[1]. Verified balances updated and Transfer event emitted.
📸 Screenshot:
![step8](transfer-confirmation.png)

✅ Step 9: Approve + TransferFrom Test
1. Approve
  . Account[0] called approve(Account[1], 1000000000000000000).
  . Verified Approval event emitted. 
2. TransferFrom
  . Account[1] (spender) called transferFrom(Account[0], Account[2], 1000000000000000000).
  . Verified balances updated and Transfer event emitted. 📸 Screenshot:
![step9](validation.png)

✅ Step 10: Approve + TransferFrom (Delegated Transfers)
. Account[0] approved Account[1] to spend 1 token.
. Account[1] used transferFrom() to send 1 token from Account[0] → Account[2].
. Balances updated correctly, allowance reduced to 0.
. Events emitted:
   Approval(owner=Account[0],spender=Account[1], . value=1000000000000000000)
   Transfer(from=Account[0], to=Account[2], value=1000000000000000000)
📸 Screenshots:
![step 10](balance-after.png)

✅ Git Commit Log
git add src/ contracts/ README.md screenshots/step8/ screenshots/step9/ screenshots/step10/
git commit -m "Steps 1–10 complete: CCOL pipeline + ERC-20 delegated transfers"
git push origin main





