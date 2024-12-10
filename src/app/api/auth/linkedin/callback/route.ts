import { NextResponse } from 'next/server';
import { cookies } from 'next/headers';

export async function GET(request: Request) {
	const { searchParams } = new URL(request.url);
	const code = searchParams.get('code');
	const state = searchParams.get('state');

	if (!code) {
		return NextResponse.redirect(`${process.env.NEXT_PUBLIC_BASE_URL}?error=no_code`);
	}

	try {
		// Exchange code for access token
		const tokenResponse = await fetch('https://www.linkedin.com/oauth/v2/accessToken', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/x-www-form-urlencoded',
			},
			body: new URLSearchParams({
				grant_type: 'authorization_code',
				code,
				client_id: process.env.LINKEDIN_CLIENT_ID!,
				client_secret: process.env.LINKEDIN_CLIENT_SECRET!,
				redirect_uri: `${process.env.NEXT_PUBLIC_BASE_URL}/api/auth/linkedin/callback`,
			}),
		});

		const tokenData = await tokenResponse.json();

		if (!tokenResponse.ok) {
			throw new Error('Failed to get access token');
		}

		// Get user profile
		const profileResponse = await fetch('https://api.linkedin.com/v2/userinfo', {
			headers: {
				Authorization: `Bearer ${tokenData.access_token}`,
			},
		});

		const profileData = await profileResponse.json();

		if (!profileResponse.ok) {
			throw new Error('Failed to get profile');
		}

		// Set session cookie
		const cookieStore = await cookies();
		cookieStore.set('session', JSON.stringify({
			accessToken: tokenData.access_token,
			user: {
				id: profileData.sub,
				name: profileData.name,
				email: profileData.email,
				picture: profileData.picture,
			}
		}), {
			httpOnly: true,
			secure: process.env.NODE_ENV === 'production',
			sameSite: 'lax',
			maxAge: 60 * 60 * 24 * 7, // 1 week
		});

		return NextResponse.redirect(`${process.env.NEXT_PUBLIC_BASE_URL}/dashboard`);
	} catch (error) {
		console.error('Auth error:', error);
		return NextResponse.redirect(`${process.env.NEXT_PUBLIC_BASE_URL}?error=auth_failed`);
	}
}