"use strict";
const rooms = [];
function addRoom(room) {
    rooms.push(room);
}
addRoom({
    id: 1,
    name: "Deluxe",
    description: "Spacious room with sea view",
    capacity: 2,
    price_per_night: 2500,
    image_url: "/images/room1.jpg",
    is_active: true
});
addRoom({
    id: 2,
    name: "Standard",
    description: "Comfortable room with city view",
    capacity: 2,
    price_per_night: 1800,
    image_url: "/images/room2.jpg",
    is_active: true
});
addRoom({
    id: 3,
    name: "Family",
    description: "Large room suitable for families",
    capacity: 4,
    price_per_night: 3200,
    image_url: "/images/room3.jpg",
    is_active: true
});
addRoom({
    id: 4,
    name: "Economy",
    description: "Basic room with essential amenities",
    capacity: 1,
    price_per_night: 1200,
    image_url: "/images/room4.jpg",
    is_active: false
});
// console.log(`${rooms[0]}`);
// console.log(`${rooms[1]}`);
function printRooms() {
    for (let i = 0; i < rooms.length; i++) {
        console.log(`---------------`);
        console.log(`ID: ${rooms[i].id}`);
        console.log(`Name: ${rooms[i].name}`);
        console.log(`Description: ${rooms[i].description}`);
        console.log(`Capacity: ${rooms[i].capacity}`);
        console.log(`Price: ${rooms[i].price_per_night}`);
        console.log(`Active: ${rooms[i].is_active}`);
    }
}
printRooms();
