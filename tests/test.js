import http from 'k6/http'
import { sleep } from 'k6';

//export const options = {
//	iterations: 100,
//};

const TOTAL_RPS = 500;
const DURATION = '1m';
function rate(percentage) {
	return TOTAL_RPS * percentage;
}

export const options = {
	scenarios: {
		busy_endpoint: {
			exec: 'testBusyEndpoint',
			executor: 'constant-arrival-rate',
			duration: '1m',
			rate: rate(0.9),
			timeUnit: '1s',
			preAllocatedVUs: 50,
			maxVUs: 100,
			duration: DURATION
		}
	}
}

export function testBusyEndpoint() {
	http.get('http://web:8000/users')
}
