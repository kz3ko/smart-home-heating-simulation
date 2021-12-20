import houseConfig from '../house-config.json';
export function getBackgroundColor(temperature) {
    const temp = Number.parseFloat(temperature)
    if (temp >= houseConfig.coldThreshold[0] && temp < houseConfig.coldThreshold[1]) {
        return 'rgba(0, 100, 255, 0.2)';
    } else if (temp >= houseConfig.optimalThreshold[0] && temp < houseConfig.optimalThreshold[1]) {
        return 'rgba(0, 255, 0, 0.3)';
    } else if (temp >= houseConfig.warmThreshold[0] && temp < houseConfig.warmThreshold[1]) {
        return 'rgba(255, 255, 0, 0.3)';
    } else if (temp >= houseConfig.hotThreshold[0]) {
        return 'rgba(255, 0, 0, 0.3)';
    }
};