import React, { useEffect, useState } from "react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from "recharts";



const StocksGraph: React.FC = () => {
    const [portfolio, setPortfolio] = useState({ holdings: [], positions: [] });

    useEffect(() => {
        fetch("http://localhost:5000/portfolio")
            .then((response) => response.json())
            .then((data) => setPortfolio(data));
    }, []);

    return (
        <div className="flex flex-row space-y-4">
            <h2>Holdings - Bar Chart</h2>
            <ResponsiveContainer width="100%" height={300}>
                <BarChart data={portfolio.holdings}>
                    <XAxis dataKey="symbol" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="current_value" fill="#8884d8" name="Current Value" />
                    <Bar dataKey="invested_amount" fill="#82ca9d" name="Invested Amount" />
                </BarChart>
            </ResponsiveContainer>

            <h2>Positions - Bar Chart</h2>
            <ResponsiveContainer width="100%" height={300}>
                <BarChart data={portfolio.positions}>
                    <XAxis dataKey="symbol" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="current_value" fill="#FF5733" name="Current Value" />
                    <Bar dataKey="invested_amount" fill="#33FF57" name="Invested Amount" />
                </BarChart>
            </ResponsiveContainer>
        </div>
    );
};
    export default StocksGraph;