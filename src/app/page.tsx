'use client';

import { useRouter } from 'next/navigation';

function Header() {
	return (
		<div>
			<h1 className="text-3xl font-bold text-center text-gray-900">
				LinkedIn Sales Analytics
			</h1>
			<p className="mt-2 text-center text-gray-600">
				Track and analyze your LinkedIn sales efforts
			</p>
		</div>
	);
}

function SignInButton({ onClick }: { onClick: () => void }) {
	return (
		<button
			onClick={onClick}
			className="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
		>
			Sign in with LinkedIn
		</button>
	);
}

export default function Home() {
	const router = useRouter();

	const handleSignIn = async () => {
		try {
			const response = await fetch('/api/auth/linkedin');
			const { url } = await response.json();
			window.location.href = url;
		} catch (error) {
			console.error('Failed to initiate LinkedIn sign in:', error);
		}
	};

	return (
		<div className="min-h-screen flex items-center justify-center bg-gray-100">
			<div className="max-w-md w-full space-y-8 p-8 bg-white rounded-lg shadow">
				<Header />
				<SignInButton onClick={handleSignIn} />
			</div>
		</div>
	);
}
