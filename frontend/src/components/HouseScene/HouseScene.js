import React, {useEffect, useState} from 'react';
import styled from "styled-components";
import houseImage from '../../assets/22428951-plan-mieszkania.jpeg';
import RoomComponent from "../Rooms/RoomComponent";
import TextInput from "../Atoms/TextInput/TextInput";
import Button from "../Atoms/Button/Button";
import config from '../../config.json';
import axios from "axios";

const houseConfig = config.house

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
  width: 800px;
  justify-content: space-around;
  align-items: center;
  margin-top: 20px;
`;

const StyledTimeLabel = styled.p`
  font-size: 35px;
  margin-left: 850px;
  margin-top: 75px;
  font-weight: bold;
`;

const HouseScene = () => {
    const [roomsData, setRoomsData] = useState(null);
    const [dateTime, setDateTime] = useState(null);
    const [selectedRoom, setSelectedRoom] = useState(null);
    const [temperature, setTemperature] = useState(null);
    const [outsideTemp, setOutsideTemp] = useState(null);

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
            console.log(res.data.roomsData)
        })
    }
    function fetchDateTime() {
        axios.get('http://localhost:8000/datetime').then(res => {
            setDateTime(res.data.dateTime)
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

    function setPeopleMoving() {
        axios.post(`http://localhost:8000/settings`, {
            peopleMove: true
        }).then(() => alert('Ruch ludzi włączony'));
    }

    function setPeopleNotMoving() {
        axios.post(`http://localhost:8000/settings`, {
            peopleMove: false
        }).then(() => alert('Ruch ludzi wyłączony'));
    }

    function turnOnLoggingToCSV() {
        axios.post(`http://localhost:8000/settings`, {
            csvLoggerEnabled: true
        }).then(() => alert('Logowanie do pliku CSV włączone.'));
    }

    function turnOffLoggingToCSV() {
        axios.post(`http://localhost:8000/settings`, {
            csvLoggerEnabled: false
        }).then(() => alert('Logowanie do pliku CSV wyłączone.'));
    }

    function setBackyardTemperature() {
        axios.post(`http://localhost:8000/settings`, {
            backyardTemperature: outsideTemp
        }).then(() => alert('Temperatura otoczenia zmieniona')).finally(() => setOutsideTemp(null));
    }

    function fetchCyclical() {
        setInterval(() => {
            fetchRoomsData()
        }, 1000)
        setInterval(() => {
            fetchDateTime()
        }, 250)
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
                            START SIMULATION
                        </button>
                        <button
                            onClick={() => stopSimulation()}
                            style={{ backgroundColor: '#ef3333' }}
                        >
                            STOP SIMULATION
                        </button>
                        <div style={{ display: 'flex', flexDirection: 'column' }}>
                            <button
                                onClick={() => setPeopleMoving()}
                                style={{ backgroundColor: '#dadada' }}
                            >
                                PEOPLE ON
                            </button>
                            <button
                                onClick={() => setPeopleNotMoving()}
                                style={{ backgroundColor: '#dadada' }}
                            >
                                PEOPLE OFF
                            </button>
                        </div>
                        <div style={{ display: 'flex', flexDirection: 'column' }}>
                            <button
                                onClick={() => turnOnLoggingToCSV()}
                                style={{ backgroundColor: '#dadada' }}
                            >
                                LOGGING ON
                            </button>
                            <button
                                onClick={() => turnOffLoggingToCSV()}
                                style={{ backgroundColor: '#dadada' }}
                            >
                                LOGGING OFF
                            </button>
                        </div>
                        <div style={{ display: 'flex', flexDirection: 'column' }}>
                            <input
                                placeholder={'Outside temperature'}
                                onChange={e => setOutsideTemp(e.target.value)}
                                value={outsideTemp}
                            />
                            <button
                                onClick={() => setBackyardTemperature()}
                                style={{ backgroundColor: '#dadada' }}
                                disabled={!outsideTemp}
                            >
                                SET
                            </button>
                        </div>
                    </StyledButtonsContainer>
                    <StyledTimeLabel>{`${dateTime}`}</StyledTimeLabel>
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
