"use client"
import React, { useEffect, useState } from 'react';
import Plot from 'react-plotly.js';

const RenderContainerData = ({ containerData }) => {
    const [plotData, setPlotData] = useState(null);

    useEffect(() => {
        if (containerData) {
            const data = [];
            containerData.boxes.forEach((boxData) => {
                const box = boxData.box;
                const location = boxData.location;
                const color = '#' + Math.floor(Math.random() * 16777215).toString(16); // Generate random color

                const boxPlotDef = {
                    type: 'scatter3d',
                    mode: 'markers',
                    x: [location.x],
                    y: [location.y],
                    z: [location.z],
                    marker: {
                        size: [box.length, box.width, box.height],
                        color: color,
                        opacity: 0.6,
                    },
                };

                data.push(boxPlotDef);
            });

            setPlotData(data);
        }
    }, [containerData]);

    return (
        <div>
            {plotData && (
                <Plot
                    data={plotData}
                    layout={{
                        width: 800,
                        height: 600,
                        scene: {
                            xaxis: { title: 'X' },
                            yaxis: { title: 'Y' },
                            zaxis: { title: 'Z' },
                        },
                        title: '3D Box Plot',
                    }}
                />
            )}
        </div>
    );
};

export default RenderContainerData;
