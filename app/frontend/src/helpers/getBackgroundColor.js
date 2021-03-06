export function getBackgroundColor(
    temperature,
    optimalThreshold,
    coldThreshold,
    warmThreshold,
    hotThreshold,
    coldDownTemp,
    numberOfPeoples
) {
    const temp = temperature.toFixed(2);
    if (numberOfPeoples === 0) {
        const warmHotDiff = (warmThreshold[1] - warmThreshold[0])
        if (temp < coldDownTemp - 0.3) {
            return 'rgba(0, 100, 255, 0.2)';
        } else if (temp > coldDownTemp && temp <= coldDownTemp + warmHotDiff) {
            return 'rgba(255, 255, 0, 0.3)';
        } else if (temp > coldDownTemp + warmHotDiff) {
            return 'rgba(255, 0, 0, 0.3)';
        } else {
            return 'rgba(0, 255, 0, 0.3)';
        }
    }

    if (temp >= coldThreshold[0] && temp < coldThreshold[1]) {
        return 'rgba(0, 100, 255, 0.2)';
    } else if (temp >= optimalThreshold[0] && temp <= optimalThreshold[1]) {
        return 'rgba(0, 255, 0, 0.3)';
    } else if (temp > warmThreshold[0] && temp < warmThreshold[1]) {
        return 'rgba(255, 255, 0, 0.3)';
    } else if (temp >= hotThreshold[0]) {
        return 'rgba(255, 0, 0, 0.3)';
    }
};