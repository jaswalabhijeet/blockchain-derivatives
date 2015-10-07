[![Build Status](https://travis-ci.org/billmarino2/blockchain-derivatives.svg?branch=master)](https://travis-ci.org/billmarino2/blockchain-derivatives)
## Blockchain Derivatives

This tool lets you enter the terms of a derivatives contract (future, option, swap, etc.) using an easy-to-use webpage interface. It then immediately converts the terms you have entered into a script in Solidity, one of the languages of Ethereum (probably the most advanced smart contract blockchain). 

What you can do next is copy and paste the Solidity script that is produced into the data field of a new transaction. Once you send that transaction, your contracted will be compiled into a block. Your contract is now live the blockchain!

### Stuff You’ll Need Besides This Tool
In order to inject contracts on the blockchain, you’ll need one of the Ethereum clients on your machine. I recommend Alethzero, the C++ GUI. You can clone Alethzero [here](https://github.com/ethereum/cpp-ethereum/wiki/Using-AlethZero).

If you prefer, you can also use Geth, the Go CLI for Ethereum, or Eth, its C++ CLI. Read about how to get those [here](https://www.ethereum.org/cli).

Lastly, you’ll need some ether. All contracts run on gas, which is paid for with ether. Read about how to get ether [here](https://www.ethereum.org/ether).

### Future Build-outs
Soon I’ll be adding features that let you keep track of the contracts you’ve built. This is important because Ethereum contracts cannot yet “wake up” on a schedule. For example, as I explain on the Ethereum Futures online form, when the maturity date on your contract arrives, you’ll have send a follow-up transaction that calls the maturity date functions in your initial contract. Eventually, I’ll be building tools to help you manage that process.

Ideally, I’ll also be giving you a way to directly injection your contracts onto the Ethereum blockchain through my platform. That’s a more ambitious goal, so wish me luck!

### This Project’s Background
This project was produced in connection with Startup Systems, an excellent engineering class I am taking at Cornell Tech. Be sure to check out the class’ [GitHub](https://github.com/Cornell-CS5356-Fall2015/cs5356).













