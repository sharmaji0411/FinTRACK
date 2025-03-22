export interface Asset {
  id: string;
  name: string;
  symbol: string;
  amount: number;
  value: number;
  change24h: number;
}

export interface PortfolioData {
  timestamp: number;
  value: number;
}

export interface MarketNews {
  id: string;
  title: string;
  source: string;
  timestamp: number;
}