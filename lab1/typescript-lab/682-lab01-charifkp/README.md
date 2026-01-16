[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/ZGd-NzYi)
# Faculty of Information and Communication Technology <br/> ITCS258 Backend Application Development <br/> Basic TypeScript

## Objective

Students will be able to set up a basic TypeScript project and implement simple interfaces and functions.

## Instruction
### Part 1: Setting Up a TypeScript Project

Follow the steps below to set up a basic TypeScript project
1. Install TypeScript globally using `npm`. **Note**: Node.js is required
   
    ```bash
    npm install -g typescript
    ```
    Note: If you use Mac and got erros, you may need to use `sudo`
   
3. Create a new project directory and navigate to it:
    
    ```bash
    mkdir typescript-lab
    cd typescript-lab
    ```
    
4. Initialize a new `npm` project with default settings:
    
    ```bash
    npm init -y
    ```
    
5. Create a `tsconfig.json` file with the following configurations:

   ```bash
   tsc --init
   ```
   Edit tsconfig.json file to the following simple setup:
    
    ```json
    {
      "compilerOptions": {
        "target": "es2016",
        "module": "commonjs",
        "outDir": "./dist",
        "rootDir": "./src",
        "strict": true,
        "esModuleInterop": true,
        "skipLibCheck": true,
        "forceConsistentCasingInFileNames": true
      },
      "include": ["src/**/*"]
    }
    ```
    
7. Create a `src` directory to store your TypeScript files:
    
    ```bash
    mkdir src
    ```

**Expected Project Structure will be:**
   ```
   typescript-lab/
   ├── src/
   ├── dist/        (generated later)
   ├── tsconfig.json
   └── package.json
   ```
    
### Part 2: Writing Your First TypeScript File - Interface and Functions
1. Inside the `src` directory, create a new file named `room.ts.`

2. Define a TypeScript interface named `Room` that represents the data dictionary below.
   The following table describes the data structure for a **Room** in the hotel booking system.

   | Field | Data Type | Description |
   |------|----------|-------------|
   | `id` | int (PK) | Primary key, auto-incremented room ID |
   | `name` | varchar(100) | Unique name or number of the room |
   | `description` | text | Description of the room and amenities |
   | `capacity` | int | Maximum number of guests |
   | `price_per_night` | decimal(10,2) | Price per night |
   | `image_url` | text | URL/path to the stored room image |
   | `is_active` | boolean | Indicates whether the room is available |


   **Note for TS conventions**:
   - Convert database-style field names (snake_case) into camelCase for TypeScript.
   - Use appropriate TypeScript data types including `number`, `string`, `boolean`, or `Date`

   ```tsx
   // Define the shape of Room
   interface Room {
     
   }
   ```

3. Create a constant `rooms` to store our room data
   ```tsx
   const rooms: Room[] = [];  
   
   ```

   Then, create a function `addRoom` with the following code:
   
   ```tsx
   function addRoom(room: Room): void {
     rooms.push(room);
   }
   ```

5. In this step, you will convert each row from the room data table into a `Room` object and add it to the system using the `addRoom()` function.
   
   | id | name          | description                         | capacity | pricePerNight | imageUrl          | isActive |
   | -- | ------------- | ----------------------------------- | -------- | ------------- | ----------------- | -------- |
   | 1  | Deluxe Room   | Spacious room with sea view         | 2        | 2500          | /images/room1.jpg | true     |
   | 2  | Standard Room | Comfortable room with city view     | 2        | 1800          | /images/room2.jpg | true     |
   | 3  | Family Room   | Large room suitable for families    | 4        | 3200          | /images/room3.jpg | true     |
   | 4  | Economy Room  | Basic room with essential amenities | 1        | 1200          | /images/room4.jpg | false    |

Example
   ```tsx
   addRoom({
     id: 1,
     name: "Deluxe Room",
     ...
   
   });
   
   ```

5. Print all room objects currently stored in the array `rooms`
   ```tsx
   console.log(`${rooms}`);
   ```

6. Compile `room.ts` to generate `room.js` by using
   ```bash
   npx tsc
   ```
 
   **Expected Project Structure will be:**
   ```
   typescript-lab/
   ├── src/
   │   └── room.ts       # Room interface definition
   ├── dist/             # Compiled JavaScript files (generated if using tsc)
   │   └── room.js       # Generated .js code
   ├── tsconfig.json      
   └── package.json
   ```

7. Run your JavaScript file:
    
    ```bash
    node dist/room.js
    ```
  **Expected Output:**
   ```bash
   [object Object],[object Object],[object Object],[object Object]
   ```

### Part 3: Fix Your TypeScript Functions
From the previous Lab section, the output from `console.log()` gives:

   ```bash
   [object Object],[object Object],[object Object],[object Object]
   ```
This happens because JavaScript does not know how to display objects when they are inside an array.

1. Modify your `room.ts` to print out all rooms properly, including

   ```tsx
   function printRooms(): void;  
   function printRooms(): void;
   ```
   **Note:**
    - printRoom(room: Room) is a function that accepts a Room object and prints its details.
    - printRooms() is a function that prints all rooms stored in the array.

2. After writing those functions, use the function `printRoomes()` to print all room data

   ```tsx
   printRooms();
   ```
3.  Compile `room.ts` and run `room.js`
   ```bash
   npx tsc
   node dist/room.js
   ```

   **Expected Output:**  (You can customize the printout text)
   ```bash
   ---------------
   ID: 1
   Name: Deluxe Room
   Description: Spacious room with sea view
   Capacity: 2
   Price: 2500
   Active: true
   ---------------
   ID: 2
   Name: Standard Room
   Description: Comfortable room with city view
   Capacity: 2
   Price: 1800
   Active: true
   ---------------
   ID: 3
   Name: Family Room
   Description: Large room suitable for families
   Capacity: 4
   Price: 3200
   Active: true
   ---------------
   ID: 4
   Name: Economy Room
   Description: Basic room with essential amenities
   Capacity: 1
   Price: 1200
   Active: false
   ```
 

## Submission

1. **Include a Generative AI usage declaration and reflection** at the beginning of your code file. Clearly state if AI tools were used and briefly reflect on your work.
2. **Push your code** to the provided GitHub Classroom repository for this assignment. Make sure all your code is committed and pushed before the submission deadline.
3. Submit the lab by the end of the next class session to the LAs. Late submissions may not be accepted.

## AI Usage Declaration and Reflection

Students must add an AI Declaration and Reflection of Today's Learning to the top of their code file.

A reflection is not a summary of what you did or what the AI generated.
Instead, it is a personal explanation of your learning process.

- If you used AI, focus on how AI impacted your learning or understanding of the code.
- If you did not use AI, focus on your learning, tools, and experience from the lab.

Here are examples:

### Example 1 – No AI Used

```tsx
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

```

### Example 2 – AI Used for Reference

```tsx
/*
AI Declaration:
I used <ChatGPT> only to clarify <something>
No code was directly copied without modification.

Reflection:
[ Write 1–2 sentences reflecting on your learning or how AI impacted your understanding]
*/

```

### Example 3 – AI Assisted in Debugging

```tsx
/*
AI Declaration:
I used <ChatGPT> to help <something>.
I wrote all the other code, and I understand the entire implementation.

Reflection:
[ Write 1–2 sentences reflecting on your learning or how AI impacted your understanding ]
*/

```
