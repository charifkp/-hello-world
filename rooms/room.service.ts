import { Injectable } from '@nestjs/common';
import { Room } from './room.interface';



@Injectable()
export class RoomService {
    private rooms: Room[] = [
        {
            id:1,
            name: "Deluxe Room",
            description: "Spacious room with sea view",
            capacity: 2,
            pricePerNight: 2500,
            imageUrl: "/images/room1.jpg",
            isActive: true

        },
        {
            id:2,
            name: "Standard Room",
            description: "Comfortable room with city view",
            capacity: 2,
            pricePerNight: 1800,
            imageUrl: "/images/room2.jpg",
            isActive: true
        },
        {
            id:3,
            name: "	Family Room",
            description: "Large room suitable for families",
            capacity: 4,
            pricePerNight: 3200,
            imageUrl: "/images/room3.jpg",
            isActive: true
        },
        {
            id:4,
            name: "Economy Room",
            description: "Basic room with essential amenities",
            capacity: 1,
            pricePerNight: 1200,
            imageUrl: "/images/room4.jpg",
            isActive: false
        }
    ];



  getAllRooms(): Room[] {
    return this.rooms;
  }




  
}
