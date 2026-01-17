import { Injectable, NotFoundException } from '@nestjs/common';
import { CreateRoomDto } from './dto/create-room.dto';
import { UpdateRoomDto } from './dto/update-room.dto';

@Injectable()
export class RoomService {
  private rooms: CreateRoomDto[] = [];
   
  create(createRoomDto: CreateRoomDto) {
    
    this.rooms.push(createRoomDto);
    
  }

  findAll():CreateRoomDto[] {
    return  this.rooms;
  }

  findOne(id: number) {
    for (let i=0;i < this.rooms.length; i++){
      if(this.rooms[i].id === id){
        return this.rooms[i];
      }
    }
    throw new NotFoundException(`Rooms with id ${id} not found`);
  }

  update(id: number, updateRoomDto: UpdateRoomDto) {
    return `This action updates a #${id} room`;
  }

  remove(id: number) {
    for (let i=0;i < this.rooms.length; i++){
      if(this.rooms[i].id === id){
        this.rooms.splice(i,1);
        return ;
      }
    }
    throw new NotFoundException(`Rooms with id ${id} not found`);
  }
}
