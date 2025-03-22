import React from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import { format } from 'date-fns';
import { Wallet, TrendingUp, Newspaper, Bell } from 'lucide-react';
import { PortfolioData, Asset, MarketNews } from '../types';
import Stocks from './Stocks';
import StocksGraph from './StocksGraph';

const mockPortfolioData: PortfolioData[] = Array.from({ length: 30 }, (_, i) => ({
  timestamp: Date.now() - (29 - i) * 24 * 60 * 60 * 1000,
  value: 50000 + Math.random() * 10000
}));

const mockAssets: Asset[] = [
  { id: '1', name: 'Bitcoin', symbol: 'BTC', amount: 0.5, value: 25000, change24h: 2.5 },
  { id: '2', name: 'Ethereum', symbol: 'ETH', amount: 4.2, value: 12600, change24h: -1.2 },
  { id: '3', name: 'Apple Inc.', symbol: 'AAPL', amount: 10, value: 1750, change24h: 0.8 },
];

const mockNews: MarketNews[] = [
  {
    id: '1',
    title: 'Stock Market Highlights: Sensex extends winning streak to day 5, ends 557 pts higher, Nifty tops 23,350 - The Economic Times',
    source: 'Financial Times',
    timestamp: Date.now() - 2 * 60 * 60 * 1000,
  },
  {
    id: '2',
    title: 'Stock Market News Today Live Updates on March 22, 2025 : Rupee hits two-month high of 85.93 against US dollar on fresh inflows, logs biggest weekly gain in over two years | Stock Market News - Mint',
    source: 'Reuters',
    timestamp: Date.now() - 4 * 60 * 60 * 1000,
  },
  {
    id: '3',
    title: 'Stock market today: BSE Sensex opens over 100 points down; Nifty50 near 23,150 - The Times of India',
    source: 'Reuters',
    timestamp: Date.now() - 4 * 60 * 60 * 1000,
  },
];

const Dashboard: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-900 text-white p-6">
      <header className="flex justify-between items-center mb-8">
        <div className="flex items-center gap-2">
          <TrendingUp className="w-8 h-8 text-emerald-400" />
          <h1 className="text-2xl font-bold">FinTRACK</h1>
        </div>
        <div className="flex items-center gap-4">
          <button className="bg-emerald-500 hover:bg-emerald-600 px-4 py-2 rounded-lg">
            Connect broker
          </button>
          <Bell className="w-6 h-6 text-gray-400 hover:text-white cursor-pointer" />
        </div>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-1 gap-6">
        <div className="lg:col-span-2 bg-gray-800 rounded-xl p-6">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl font-semibold">Portfolio Value</h2>
            <div className="flex gap-2">
              {['1D', '1W', '1M', '3M', 'YTD', '1Y'].map((period) => (
                <button
                  key={period}
                  className="px-3 py-1 rounded-lg hover:bg-gray-700 text-sm"
                >
                  {period}
                </button>
              ))}
            </div>
          </div>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={mockPortfolioData}>
              <XAxis
                dataKey="timestamp"
                tickFormatter={(timestamp) => format(timestamp, 'MMM d')}
                stroke="#6B7280"
              />
              <YAxis stroke="#6B7280" />
              <Tooltip
                contentStyle={{ backgroundColor: '#1F2937', border: 'none' }}
                formatter={(value: number) => [`$${value.toLocaleString()}`, 'Portfolio Value']}
                labelFormatter={(timestamp) => format(timestamp, 'MMM d, yyyy')}
              />
              <Line
                type="monotone"
                dataKey="value"
                stroke="#10B981"
                strokeWidth={2}
                dot={false}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-gray-800 rounded-xl p-6 ">
          <h2 className="text-xl font-semibold mb-6">Assets</h2>
          <div className="space-y-4">
            {mockAssets.map((asset) => (
              <div
                key={asset.id}
                className="flex items-center justify-between p-4 bg-gray-700 rounded-lg"
              >
                <div>
                  <div className="font-medium">{asset.name}</div>
                  <div className="text-sm text-gray-400">{asset.symbol}</div>
                </div>
                <div className="text-right">
                  <div>${asset.value.toLocaleString()}</div>
                  <div
                    className={`text-sm ${
                      asset.change24h >= 0 ? 'text-emerald-400' : 'text-red-400'
                    }`}
                  >
                    {asset.change24h >= 0 ? '+' : ''}
                    {asset.change24h}%
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="App text-center ">
       <StocksGraph/>
       <Stocks />
    </div>

        <div className="lg:col-span-3 bg-gray-800 rounded-xl p-6">
          <h2 className="text-xl font-semibold mb-6">Market News</h2>
          <div className="space-y-4">
            {mockNews.map((news) => (
              <div
                key={news.id}
                className="flex items-start gap-4 p-4 bg-gray-700 rounded-lg cursor-pointer hover:bg-gray-600"
              >
                <Newspaper className="w-5 h-5 text-emerald-400 mt-1" />
                <div>
                  <div className="font-medium">{news.title}</div>
                  <div className="text-sm text-gray-400 mt-1">
                    {news.source} • {format(news.timestamp, 'h:mm a')}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;