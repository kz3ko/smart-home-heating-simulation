import React, {useState} from 'react';
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

const StyledHouseScene = styled.div`
  display: flex;
  width: ${houseConfig.pageWidth}px;
  height: ${houseConfig.pageHeight}px;
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

const HouseScene = () => {
    const [dialogVisible, setDialogVisible] = useState(null);
    const [temperature, setTemperature] = useState(null);
    const [bedroomTemp, setBedroomTemp] = useState('26,4');
    const [officeTemp, setOfficeTemp] = useState('24.4');
    const [livingRoomTemp, setLivingRoomTemp] = useState('15');
    const [northRoomTemp, setNorthRoomTemp] = useState('22.3');
    const [southRoomTemp, setSouthRoomTemp] = useState('21.5');
    const [bathRoomTemp, setBathRoomTemp] = useState('24.6');

    function changeTemperature() {
        if (temperature) {
            switch(dialogVisible) {
                case 'bedroom':
                    setBedroomTemp(temperature);
                    setDialogVisible(null);
                    setTemperature(null);
                    break;
                case 'officeroom':
                    setOfficeTemp(temperature);
                    setDialogVisible(null);
                    setTemperature(null);
                    break;
                case 'livingroom':
                    setLivingRoomTemp(temperature);
                    setDialogVisible(null);
                    setTemperature(null);
                    break;
                case 'northroom':
                    setNorthRoomTemp(temperature);
                    setDialogVisible(null);
                    setTemperature(null);
                    break;
                case 'southroom':
                    setSouthRoomTemp(temperature);
                    setDialogVisible(null);
                    setTemperature(null);
                    break;
                case 'bathroom':
                    setBathRoomTemp(temperature);
                    setDialogVisible(null);
                    setTemperature(null);
                    break;
            }
        } else {
            setDialogVisible(null);
        }
    }

    return (
        <StyledHouseScene style={{
            backgroundImage: `url(${houseImage}`,
            backgroundPosition: 'center',
            backgroundSize: 'contain',
            backgroundRepeat: 'no-repeat'
        }}>
            <Room1
                temperature={bedroomTemp}
                dialogVisible={setDialogVisible}
                width={houseConfig.rooms.bedRoom.width}
                height={houseConfig.rooms.bedRoom.height}
                xPos={houseConfig.rooms.bedRoom.xPos}
                yPos={houseConfig.rooms.bedRoom.yPos}
            />
            <OfficeRoom
                temperature={officeTemp}
                dialogVisible={setDialogVisible}
                width={houseConfig.rooms.officeRoom.width}
                height={houseConfig.rooms.officeRoom.height}
                xPos={houseConfig.rooms.officeRoom.xPos}
                yPos={houseConfig.rooms.officeRoom.yPos}
            />
            <LivingRoom
                temperature={livingRoomTemp}
                dialogVisible={setDialogVisible}
                width={houseConfig.rooms.livingRoom.width}
                height={houseConfig.rooms.livingRoom.height}
                xPos={houseConfig.rooms.livingRoom.xPos}
                yPos={houseConfig.rooms.livingRoom.yPos}
            />
            <BathRoom
                temperature={bathRoomTemp}
                dialogVisible={setDialogVisible}
                width={houseConfig.rooms.bathRoom.width}
                height={houseConfig.rooms.bathRoom.height}
                xPos={houseConfig.rooms.bathRoom.xPos}
                yPos={houseConfig.rooms.bathRoom.yPos}
            />
            <NorthRoom
                temperature={northRoomTemp}
                dialogVisible={setDialogVisible}
                width={houseConfig.rooms.northRoom.width}
                height={houseConfig.rooms.northRoom.height}
                xPos={houseConfig.rooms.northRoom.xPos}
                yPos={houseConfig.rooms.northRoom.yPos}
            />
            <SouthRoom
                temperature={southRoomTemp}
                dialogVisible={setDialogVisible}
                width={houseConfig.rooms.southRoom.width}
                height={houseConfig.rooms.southRoom.height}
                xPos={houseConfig.rooms.southRoom.xPos}
                yPos={houseConfig.rooms.southRoom.yPos}
            />
            {dialogVisible && (
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
                            <Button disabled={temperature < 15 || temperature > 30} onClick={() => changeTemperature()}>
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
            )}
        </StyledHouseScene>
    );
};

export default HouseScene;
