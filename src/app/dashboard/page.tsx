'use client';

import { format, subDays } from 'date-fns';
import { useEffect, useState } from 'react';
import ConnectionFunnelChart from './components/ConnectionFunnelChart';
import DateRangeSelector from './components/DateRangeSelector';
import Header from './components/Header';

interface Session {
	user: {
		name: string;
		email: string;
		picture: string;
	};
	accessToken: string;
}

export default function Dashboard() {
	const [session, setSession] = useState<Session | null>(null);
	const [dateRange, setDateRange] = useState({
		start: format(subDays(new Date(), 30), 'yyyy-MM-dd'),
		end: format(new Date(), 'yyyy-MM-dd'),
	});

	useEffect(() => {
		// Check session on component mount
		fetch('/api/auth/session')
			.then(res => res.json())
			.then(data => {
				if (!data.session) {
					window.location.href = '/';
				} else {
					setSession(data.session);
				}
			})
			.catch(() => {
				window.location.href = '/';
			});
	}, []);

	// Mock data - will be replaced with real LinkedIn API data
	const data = [
		{
			name: 'Conversion Funnel',
			'Requests Sent': 100,
			'Accepted Connections': 65,
			'Active Conversations': 30,
		},
	];

	if (!session) {
		return null;
	}

	return (
		<main className="min-h-screen bg-gray-100 p-8 max-w-7xl mx-auto">
			<Header user={session.user} />
			<DateRangeSelector dateRange={dateRange} setDateRange={setDateRange} />
			<ConnectionFunnelChart data={data} />
		</main>
	);
}