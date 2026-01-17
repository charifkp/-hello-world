import { Controller, Get, Post, Body, Patch, Param, Delete } from '@nestjs/common';
import { RoomService } from './room.service';
import { CreateRoomDto } from './dto/create-room.dto';
import { UpdateRoomDto } from './dto/update-room.dto';

@Controller('room')
export class RoomController {
  constructor(private readonly roomService: RoomService) {}

  @Post('/rooms')
  create(@Body() createRoomDto: CreateRoomDto) {
    return this.roomService.create(createRoomDto);
  }

  @Get('/rooms')
  findAll() {
    return this.roomService.findAll();
  }

  @Get('/rooms/:id')
  findOne(@Param('id') id: string) {
    return this.roomService.findOne(+id);
  }

  @Patch('/rooms:id')
  update(@Param('id') id: string, @Body() updateRoomDto: UpdateRoomDto) {
    return this.roomService.update(+id, updateRoomDto);
  }

  @Delete('/rooms/:id')
  remove(@Param('id') id: string) {
    return this.roomService.remove(+id);
  }
}
