// SPDX-License-Identifier: MIT

pragma solidity ^0.6.0;

contract SimpleStorege {
    uint256 favoriteNumber;
    bool favoriteBool;

    struct People {
        uint256 favoriteNumber;
        string name;
    }

    //one object

    //People public person = People({favoriteNumber:2, name:"Patrick"});

    //Arrays

    People[] public people;

    //Mapping

    mapping(string => uint256) public nameToFavoriteNumber;

    // public -> everyone can see the variable or the function in the contract

    function store(uint256 _favoriteNumber) public {
        favoriteNumber = _favoriteNumber;
    }

    // view -> is statement we want to read of a blockchain... blue buttons are views

    // pure -> same type of math in the function... blue buttons

    // retunrs(TYPE) -> to the functions return something

    function retrieve() public view returns (uint256) {
        return favoriteNumber;
    }

    // memory -> data will only be stored during the execution of the function

    //storege -> data will presiste after the execution of the function

    function addPerson(string memory _name, uint256 _favoriteNumber) public {
        people.push(People(_favoriteNumber, _name));

        nameToFavoriteNumber[_name] = _favoriteNumber;
    }
}
