import React, {useEffect, useState} from 'react';
import styled from "styled-components";
import houseImage from '../../assets/22428951-plan-mieszkania.jpeg';
import Room1 from "../Rooms/Room1";
import OfficeRoom from "../Rooms/OfficeRoom";
import LivingRoom from "../Rooms/LivingRoom";
import BathRoom from "../Rooms/BathRoom";
import NorthRoom from "../Rooms/NorthRoom";
import SouthRoom from "../Rooms/SouthRoom";
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
    const [dialogVisible, setDialogVisible] = useState(null);
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
                    <Button disabled={temperature < 15 || temperature > 30} onClick={() => setDialogVisible(false)}>
                        Zatwierdź
                    </Button>
                    <div style={{ width: 16 }}/>
                    <Button onClick={() => setDialogVisible(null)}>
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
            console.log(res.data.roomsData)
            setRoomsData(res.data.roomsData);
        })
    }

    function setPeopleAmount (roomId, numberOfPeople) {
        axios.post(`http://localhost:8000/update-room/${roomId}`, {
            numberOfPeople
        }).finally(() => fetchRoomsData());
    }

    function fetchCyclical() {
        setInterval(() => {
            fetchRoomsData()
        }, 3000)
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
                    <Room1
                        numberOfPeople={roomsData.filter(e => e.name === 'bedRoom')[0].numberOfPeople}
                        temperature={roomsData.filter(e => e.name === 'bedRoom')[0].currentTemperature}
                        coldThreshold={roomsData.filter(e => e.name === 'bedRoom')[0].coldThreshold}
                        optimalThreshold={roomsData.filter(e => e.name === 'bedRoom')[0].optimalThreshold}
                        warmThreshold={roomsData.filter(e => e.name === 'bedRoom')[0].warmThreshold}
                        hotThreshold={roomsData.filter(e => e.name === 'bedRoom')[0].hotThreshold}
                        dialogVisible={setDialogVisible}
                        setPeopleAmount={setPeopleAmount}
                        roomId={houseConfig.rooms.bedRoom.id}
                        width={houseConfig.rooms.bedRoom.width}
                        height={houseConfig.rooms.bedRoom.height}
                        xPos={houseConfig.rooms.bedRoom.xPos}
                        yPos={houseConfig.rooms.bedRoom.yPos}
                    />
                    <OfficeRoom
                        temperature={roomsData.filter(e => e.name === 'officeRoom')[0].currentTemperature}
                        dialogVisible={setDialogVisible}
                        numberOfPeople={roomsData.filter(e => e.name === 'officeRoom')[0].numberOfPeople}
                        coldThreshold={roomsData.filter(e => e.name === 'officeRoom')[0].coldThreshold}
                        optimalThreshold={roomsData.filter(e => e.name === 'officeRoom')[0].optimalThreshold}
                        warmThreshold={roomsData.filter(e => e.name === 'officeRoom')[0].warmThreshold}
                        hotThreshold={roomsData.filter(e => e.name === 'officeRoom')[0].hotThreshold}
                        setPeopleAmount={setPeopleAmount}
                        roomId={houseConfig.rooms.officeRoom.id}
                        width={houseConfig.rooms.officeRoom.width}
                        height={houseConfig.rooms.officeRoom.height}
                        xPos={houseConfig.rooms.officeRoom.xPos}
                        yPos={houseConfig.rooms.officeRoom.yPos}
                    />
                    <LivingRoom
                        numberOfPeople={roomsData.filter(e => e.name === 'livingRoom')[0].numberOfPeople}
                        coldThreshold={roomsData.filter(e => e.name === 'livingRoom')[0].coldThreshold}
                        optimalThreshold={roomsData.filter(e => e.name === 'livingRoom')[0].optimalThreshold}
                        warmThreshold={roomsData.filter(e => e.name === 'livingRoom')[0].warmThreshold}
                        hotThreshold={roomsData.filter(e => e.name === 'livingRoom')[0].hotThreshold}
                        temperature={roomsData.filter(e => e.name === 'livingRoom')[0].currentTemperature}
                        dialogVisible={setDialogVisible}
                        setPeopleAmount={setPeopleAmount}
                        roomId={houseConfig.rooms.livingRoom.id}
                        width={houseConfig.rooms.livingRoom.width}
                        height={houseConfig.rooms.livingRoom.height}
                        xPos={houseConfig.rooms.livingRoom.xPos}
                        yPos={houseConfig.rooms.livingRoom.yPos}
                    />
                    <BathRoom
                        numberOfPeople={roomsData.filter(e => e.name === 'bathRoom')[0].numberOfPeople}
                        coldThreshold={roomsData.filter(e => e.name === 'bathRoom')[0].coldThreshold}
                        optimalThreshold={roomsData.filter(e => e.name === 'bathRoom')[0].optimalThreshold}
                        warmThreshold={roomsData.filter(e => e.name === 'bathRoom')[0].warmThreshold}
                        hotThreshold={roomsData.filter(e => e.name === 'bathRoom')[0].hotThreshold}
                        temperature={roomsData.filter(e => e.name === 'bathRoom')[0].currentTemperature}
                        dialogVisible={setDialogVisible}
                        setPeopleAmount={setPeopleAmount}
                        roomId={houseConfig.rooms.bathRoom.id}
                        width={houseConfig.rooms.bathRoom.width}
                        height={houseConfig.rooms.bathRoom.height}
                        xPos={houseConfig.rooms.bathRoom.xPos}
                        yPos={houseConfig.rooms.bathRoom.yPos}
                    />
                    <NorthRoom
                        numberOfPeople={roomsData.filter(e => e.name === 'northRoom')[0].numberOfPeople}
                        coldThreshold={roomsData.filter(e => e.name === 'northRoom')[0].coldThreshold}
                        optimalThreshold={roomsData.filter(e => e.name === 'northRoom')[0].optimalThreshold}
                        warmThreshold={roomsData.filter(e => e.name === 'northRoom')[0].warmThreshold}
                        hotThreshold={roomsData.filter(e => e.name === 'northRoom')[0].hotThreshold}
                        temperature={roomsData.filter(e => e.name === 'northRoom')[0].currentTemperature}
                        dialogVisible={setDialogVisible}
                        setPeopleAmount={setPeopleAmount}
                        roomId={houseConfig.rooms.northRoom.id}
                        width={houseConfig.rooms.northRoom.width}
                        height={houseConfig.rooms.northRoom.height}
                        xPos={houseConfig.rooms.northRoom.xPos}
                        yPos={houseConfig.rooms.northRoom.yPos}
                    />
                    <SouthRoom
                        numberOfPeople={roomsData.filter(e => e.name === 'southRoom')[0].numberOfPeople}
                        coldThreshold={roomsData.filter(e => e.name === 'southRoom')[0].coldThreshold}
                        optimalThreshold={roomsData.filter(e => e.name === 'southRoom')[0].optimalThreshold}
                        warmThreshold={roomsData.filter(e => e.name === 'southRoom')[0].warmThreshold}
                        hotThreshold={roomsData.filter(e => e.name === 'southRoom')[0].hotThreshold}
                        temperature={roomsData.filter(e => e.name === 'southRoom')[0].currentTemperature}
                        dialogVisible={setDialogVisible}
                        setPeopleAmount={setPeopleAmount}
                        roomId={houseConfig.rooms.southRoom.id}
                        width={houseConfig.rooms.southRoom.width}
                        height={houseConfig.rooms.southRoom.height}
                        xPos={houseConfig.rooms.southRoom.xPos}
                        yPos={houseConfig.rooms.southRoom.yPos}
                    />
                    {dialogVisible && (
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
