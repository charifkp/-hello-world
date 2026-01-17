 import { Controller, Get } from '@nestjs/common';
 import { RoomService } from './room.service';
 import { Room } from './room.interface';
 
 @Controller(`room`) // TODO: define the base route here
 export class RoomController {
 
   // TODO: inject RoomService using the constructor
   constructor(private readonly roomservice: RoomService) {}
 
   // TODO: create a GET route to return all rooms
   @Get()
   getAllRooms(): Room[] {
     // TODO: call the appropriate service method
     return this.roomservice.getAllRooms();
   }
 }
