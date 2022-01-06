import React, {useEffect, useState} from 'react';
import styled from "styled-components";
import houseImage from '../../assets/22428951-plan-mieszkania.jpeg';
import RoomComponent from "../Rooms/RoomComponent";
import TextInput from "../Atoms/TextInput/TextInput";
import Button from "../Atoms/Button/Button";
import houseConfig from '../../house-config.json';
import axios from "axios";

const StyledHouseScene = styled.div`
  display: flex;
  width: ${houseConfig.pageWidth}px;
  height: ${houseConfig.pageHeight}px;
  flex-direction: column;
`;

const StyledDialog = styled.div`
  display: flex;
  width: 350px;
  height: 200px;
  background-color: white;
  border: 1px solid black;
  border-radius: 4px;
  position: absolute;
  top: 50%;
  left: 50%;
  z-index: 100;
  margin-left: -175px;
  margin-top: -100px;
  flex-direction: column;
  padding: 8px;
`;

const StyledButtonsWrapper = styled.div`
  width: 90%;
  display: flex;
  flex-direction: row;
  align-items: center;
`;

const StyledInputWrapper = styled.div`
  display: flex;
  width: 100%;
  align-items: center;
  margin-top: 8px;
  flex-direction: column;
`;

const ErrorText = styled.span`
  font-size: 16px;
  color: red;
  text-align: center;
`;

const StyledButtonsContainer = styled.div`
  display: flex;
  align-self: center;
  flex-direction: row;
  width: 400px;
  justify-content: space-around;
  align-items: center;
  margin-top: 20px;
`;

const HouseScene = () => {
    const [roomsData, setRoomsData] = useState(null);
    const [selectedRoom, setSelectedRoom] = useState(null);
    const [temperature, setTemperature] = useState(null);

    const renderDialog = () => (
        <StyledDialog>
            <span style={{ textAlign: 'center' }}>Zmień temperaturę pomieszczenia</span>
            <StyledInputWrapper>
                <div style={{ width: '60%', alignSelf: 'center' }}>
                    <TextInput
                        onChange={e => setTemperature(e.target.value)}
                        value={temperature}
                        type={'number'}
                        name={'temperature'}
                        placeholder={'Ustaw temperaturę pokoju'}
                        max={30}
                        min={15}
                    />
                </div>
                <StyledButtonsWrapper>
                    <Button disabled={temperature < 15 || temperature > 30} onClick={() => setRoomTemperature()}>
                        Zatwierdź
                    </Button>
                    <div style={{ width: 16 }}/>
                    <Button onClick={() => setSelectedRoom(null)}>
                        Anuluj
                    </Button>
                </StyledButtonsWrapper>
                {temperature > 30 || temperature < 15 && (
                    <ErrorText>
                        wybierz temperaturę z zakresu od 15 do 30
                    </ErrorText>
                )}
            </StyledInputWrapper>
        </StyledDialog>
    );

    function startSimulation() {
        axios.post('http://localhost:8000/start').then(() => alert('Symulacja rozpoczęta'));
    }
    function stopSimulation() {
        axios.post('http://localhost:8000/stop').then(() => alert('Symulacja zakończona'));
    }
    function fetchRoomsData() {
        axios.get('http://localhost:8000/rooms').then(res => {
            setRoomsData(res.data.roomsData);
            console.log(roomsData)
        })
    }

    function setRoomTemperature () {
        axios.post(`http://localhost:8000/update-room/${selectedRoom}`, {
            currentTemperature: parseFloat(temperature)
        }).finally(() => {
            setSelectedRoom(null);
            setTemperature(null);
        });
    }

    function setPeopleAmount (roomId, numberOfPeople) {
        axios.post(`http://localhost:8000/update-room/${roomId}`, {
            numberOfPeople
        }).finally(() => fetchRoomsData());
    }

    function fetchCyclical() {
        setInterval(() => {
            fetchRoomsData()
        }, 1000)
    }

    useEffect(() => {
        fetchCyclical();
    }, [])

    return (
        <>
            {roomsData ? (
                <StyledHouseScene style={{
                    backgroundImage: `url(${houseImage}`,
                    backgroundPosition: 'center',
                    backgroundSize: 'contain',
                    backgroundRepeat: 'no-repeat'
                }}>
                    <StyledButtonsContainer>
                        <button
                            onClick={() => startSimulation()}
                            style={{ backgroundColor: '#80d43c' }}
                        >
                            START
                        </button>
                        <button
                            onClick={() => stopSimulation()}
                            style={{ backgroundColor: '#ef3333' }}
                        >
                            STOP
                        </button>
                    </StyledButtonsContainer>
                    {houseConfig.rooms.map((item) => {
                        return (
                            <RoomComponent
                                numberOfPeople={roomsData.filter(e => e.name === item.name)[0].numberOfPeople}
                                temperature={roomsData.filter(e => e.name === item.name)[0].currentTemperature}
                                coldThreshold={roomsData.filter(e => e.name === item.name)[0].coldThreshold}
                                optimalThreshold={roomsData.filter(e => e.name === item.name)[0].optimalThreshold}
                                warmThreshold={roomsData.filter(e => e.name === item.name)[0].warmThreshold}
                                hotThreshold={roomsData.filter(e => e.name === item.name)[0].hotThreshold}
                                coolDownTemp={roomsData.filter(e => e.name === item.name)[0].cooldownTemperature}
                                title={item.title}
                                selectRoom={setSelectedRoom}
                                setPeopleAmount={setPeopleAmount}
                                roomId={item.id}
                                width={item.width}
                                height={item.height}
                                xPos={item.xPos}
                                yPos={item.yPos}
                            />
                        )
                    })}
                    {selectedRoom && (
                        renderDialog()
                    )}
                </StyledHouseScene>
            ) : (
                <span>Loading...</span>
            )}
        </>
    );
};

export default HouseScene;
