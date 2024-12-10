import { NextResponse } from 'next/server';
import { generateState } from '@/lib/auth';

export async function GET() {
	const state = generateState();
	const clientId = process.env.LINKEDIN_CLIENT_ID;
	const redirectUri = encodeURIComponent(`${process.env.NEXT_PUBLIC_BASE_URL}/api/auth/linkedin/callback`);
	const scope = encodeURIComponent('openid profile email');

	const linkedInAuthUrl = `https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=${clientId}&redirect_uri=${redirectUri}&state=${state}&scope=${scope}`;

	return NextResponse.json({ url: linkedInAuthUrl });
}