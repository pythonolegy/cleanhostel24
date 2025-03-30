// src/App.tsx

import  { useEffect, useState } from 'react';
import axios from 'axios';

interface Room {
    id: number;
    name: string;
    status: string;
    price: number;
    image: string;
}

function App() {
    const [rooms, setRooms] = useState<Room[]>([]);

    useEffect(() => {
        axios.get('http://localhost:8000/rooms')  // Здесь запрос к твоему FastAPI бэкенду
            .then(response => {
                setRooms(response.data);
            })
            .catch(error => {
                console.error("There was an error fetching the rooms data!", error);
            });
    }, []);

    return (
        <div className="App">
            <h1>Rooms</h1>
            <div>
                {rooms.map(room => (
                    <div key={room.id}>
                        <h2>{room.name}</h2>
                        <p>{room.status}</p>
                        <p>{room.price}</p>
                        <img src={room.image} alt={room.name} width="100" />
                    </div>
                ))}
            </div>
        </div>
    );
}

export default App;
