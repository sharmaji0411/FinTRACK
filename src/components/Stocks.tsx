import React, { useEffect, useState } from "react";

const PortfolioTable = () => {
    interface Holding {
        symbol: string;
        quantity: number;
        invested_amount: number;
        current_value: number;
        profit_loss: number;
        profit_loss_percent: number;
    }
    
    interface Position {
        symbol: string;
        quantity: number;
        invested_amount: number;
        current_value: number;
        profit_loss: number;
        profit_loss_percent: number;
    }
    
    const [portfolio, setPortfolio] = useState<{ holdings: Holding[]; positions: Position[] }>({ holdings: [], positions: [] });

    useEffect(() => {
        fetch("http://localhost:5000/portfolio")
            .then((response) => response.json())
            .then((data) => {
                setPortfolio({
                    holdings: Array.isArray(data.holdings) ? data.holdings : [],
                    positions: Array.isArray(data.positions) ? data.positions : [],
                });
            })
            .catch((error) => {
                console.error("Error fetching portfolio data:", error);
            });
    }, []);

    return (
        <>
        <div className="lg:col-span-2 bg-gray-800 rounded-xl p-6 w-full">
            <div className="mb-6">
                <h2 className="text-xl font-semibold mb-4">Holdings</h2>
                <table className="min-w-full border-collapse border border-gray-400">
                    <thead className="bg-gray-700 text-white">
                        <tr>
                            <th className="border border-gray-400 px-4 py-2">Symbol</th>
                            <th className="border border-gray-400 px-4 py-2">Invested Amount</th>
                            <th className="border border-gray-400 px-4 py-2">Current Value</th>
                            <th className="border border-gray-400 px-4 py-2">Profit/Loss</th>
                            <th className="border border-gray-400 px-4 py-2">Profit/Loss (%)</th>
                        </tr>
                    </thead>
                    <tbody>
                        {portfolio.holdings.map((stock, index) => (
                            <tr key={index} className="text-center">
                                <td className="border border-gray-400 px-4 py-2">{stock.symbol}</td>
                                <td className="border border-gray-400 px-4 py-2">{stock.invested_amount}</td>
                                <td className="border border-gray-400 px-4 py-2">{stock.current_value}</td>
                                <td className="border border-gray-400 px-4 py-2">{stock.profit_loss}</td>
                                <td className="border border-gray-400 px-4 py-2">{stock.profit_loss_percent}%</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            <div className="mb-6">
                <h2 className="text-xl font-semibold mb-4">Positions</h2>
                <table className="min-w-full border-collapse border border-gray-400">
                    <thead className="bg-gray-700 text-white">
                        <tr>
                            <th className="border border-gray-400 px-4 py-2">Symbol</th>
                            <th className="border border-gray-400 px-4 py-2">Invested Amount</th>
                            <th className="border border-gray-400 px-4 py-2">Current Value</th>
                            <th className="border border-gray-400 px-4 py-2">Profit/Loss</th>
                            <th className="border border-gray-400 px-4 py-2">Profit/Loss (%)</th>
                        </tr>
                    </thead>
                    <tbody>
                        {portfolio.positions.map((position, index) => (
                            <tr key={index} className="text-center">
                                <td className="border border-gray-400 px-4 py-2">{position.symbol}</td>
                                <td className="border border-gray-400 px-4 py-2">{position.invested_amount}</td>
                                <td className="border border-gray-400 px-4 py-2">{position.current_value}</td>
                                <td className="border border-gray-400 px-4 py-2">{position.profit_loss}</td>
                                <td className="border border-gray-400 px-4 py-2">{position.profit_loss_percent}%</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>

        </>
    );
};

export default PortfolioTable;


