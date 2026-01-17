export interface Room {
   id: number;               // Primary key
   name: string;             // Room name or number
   description: string;      // Room description
   capacity: number;         // Maximum guests
   pricePerNight: number;    // Price per night
   imageUrl: string;         // Image URL or path
   isActive: boolean;        // Availability status
 }
 