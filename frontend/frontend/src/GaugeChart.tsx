import React from 'react';
import Gauge from 'react-d3-speedometer';

interface GaugeChartProps {
    label: string;
    value: number;
}

const GaugeChart: React.FC<GaugeChartProps> = ({ label, value }) => {
    const gaugeOptions = {
        minValue: 0,
        maxValue: 300,
        value,
        needleColor: 'grey',
        startColor: '#00b050',
        endColor: '#660066',
        segments: 6,
        currentValueText: "PM 2.5 Level",
        segmentColors: ['#00b050', '#ffc000', '#ff9900', '#ff0000', '#7030a0', '#660066'],
    };

    return (
        <>
            <h3>{label}</h3>
            <Gauge {...gaugeOptions} />
        </>
    );
};

export default GaugeChart;