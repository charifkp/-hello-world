/*
AI Declaration: 
No Generative AI tools were used for this lab.
All code was written manually by the student.

Reflection:
[ Your Reflection goes here
Today’s lab helped me learn [structure of nestjs].
I practiced about how to develop typescript in topic server with nestjs.
]
*/


import { Module } from '@nestjs/common';
import { RoomController } from './room.controller';
import { RoomService } from './room.service';

@Module({
  controllers: [RoomController],
  providers: [RoomService],
})
export class RoomModule {}


