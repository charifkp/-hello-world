// Define the shape of Room

/*
AI Declaration:
No Generative AI tools were used for this lab.
All code was written manually by the student.

Reflection:
[ Your Reflection goes here
Today’s lab helped me learn [key takeaway].
I practiced ...
]
*/


interface Room {
   id: Number,
   name: String,
   description: String,
   capacity: Number,
   price_per_night: Number,
   image_url: String,
   is_active: boolean

}

const rooms: Room[] = [
    
  ];  

function addRoom(room: Room): void {
  rooms.push(room);
}

addRoom({
    id: 1,
    name: "Deluxe",
    description:"Spacious room with sea view",
    capacity:2,
    price_per_night:2500,
    image_url:"/images/room1.jpg",
    is_active:true
})

addRoom({
    id: 2,
    name: "Standard",
    description:"Comfortable room with city view",
    capacity:2,
    price_per_night:1800,
    image_url:"/images/room2.jpg",
    is_active:true
})

addRoom({
    id: 3,
    name: "Family",
    description:"Large room suitable for families",
    capacity:4,
    price_per_night:3200,
    image_url:"/images/room3.jpg",
    is_active:true
})

addRoom({
    id: 4,
    name: "Economy",
    description:"Basic room with essential amenities",
    capacity:1,
    price_per_night:1200,
    image_url:"/images/room4.jpg",
    is_active:false
})

// console.log(`${rooms[0]}`);
// console.log(`${rooms[1]}`);

function printRooms(): void{
    for(let i=0;i<rooms.length;i++){
        console.log(`---------------`)
        console.log(`ID: ${rooms[i].id}`)
        console.log(`Name: ${rooms[i].name}`)
        console.log(`Description: ${rooms[i].description}`)
        console.log(`Capacity: ${rooms[i].capacity}`)
        console.log(`Price: ${rooms[i].price_per_night}`)
        console.log(`Active: ${rooms[i].is_active}`)

    }
}
printRooms();
