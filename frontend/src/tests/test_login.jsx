import React from 'react';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter } from 'react-router-dom';

import Login from '../Login';

describe('Login', () => {

test('renders login form', () => {
render(<Login />, { wrapper: MemoryRouter });

expect(screen.getByLabelText('Email')).toBeInTheDocument();
expect(screen.getByLabelText('Password')).toBeInTheDocument();
expect(screen.getByRole('button', { name: 'Login' })).toBeInTheDocument();
});

test('updates state on input change', () => {
render(<Login />, { wrapper: MemoryRouter });

const emailInput = screen.getByLabelText('Email');
const passwordInput = screen.getByLabelText('Password');

userEvent.type(emailInput, 'test@example.com');
expect(emailInput).toHaveValue('test@example.com');

userEvent.type(passwordInput, 'password123');
expect(passwordInput).toHaveValue('password123');
});

test('handles form submission', async () => {
const mockNavigate = jest.fn();
jest.spyOn(require('react-router-dom'), 'useNavigate').mockReturnValue(mockNavigate);

const mockPost = jest.fn().mockResolvedValue({
status: 200,
data: {
status: 'success'
}
});
jest.spyOn(require('axios'), 'post').mockImplementation(mockPost);

render(<Login />, { wrapper: MemoryRouter });

const emailInput = screen.getByLabelText('Email');
const passwordInput = screen.getByLabelText('Password');
const submitBtn = screen.getByRole('button', { name: 'Login' });

userEvent.type(emailInput, 'test@example.com');
userEvent.type(passwordInput, 'password123');
userEvent.click(submitBtn);

await expect(mockPost).toHaveBeenCalledTimes(1);
expect(mockPost).toHaveBeenCalledWith('http://127.0.0.1:5000/login', {
email: 'test@example.com',
password: 'password123'
});
expect(mockNavigate).toHaveBeenCalledWith('/home');
});

});
