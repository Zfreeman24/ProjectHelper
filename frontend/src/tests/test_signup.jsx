import React from 'react';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import Signup from '../Signup';

describe('Signup', () => {

test('renders signup form', () => {
render(<Signup />);
expect(screen.getByText('Register')).toBeInTheDocument();
expect(screen.getByLabelText('Name')).toBeInTheDocument();
expect(screen.getByLabelText('Email')).toBeInTheDocument();
expect(screen.getByLabelText('Password')).toBeInTheDocument();
expect(screen.getByRole('button', { name: 'Register' })).toBeInTheDocument();
});

test('updates state on input change', () => {
render(<Signup />);
const nameInput = screen.getByLabelText('Name');
const emailInput = screen.getByLabelText('Email');
const passwordInput = screen.getByLabelText('Password');

userEvent.type(nameInput, 'John');
expect(nameInput).toHaveValue('John');

userEvent.type(emailInput, 'john@test.com');
expect(emailInput).toHaveValue('john@test.com');

userEvent.type(passwordInput, 'password123');
expect(passwordInput).toHaveValue('password123');
});

test('handles form submission', async () => {
// Mock API call
const mockPost = jest.fn();
jest.spyOn(require('axios'), 'post').mockImplementation(mockPost);

render(<Signup />);
const nameInput = screen.getByLabelText('Name');
const emailInput = screen.getByLabelText('Email');
const passwordInput = screen.getByLabelText('Password');
userEvent.type(nameInput, 'John');
userEvent.type(emailInput, 'john@test.com');
userEvent.type(passwordInput, 'password123');

const submitBtn = screen.getByRole('button', { name: 'Register' });
userEvent.click(submitBtn);

expect(mockPost).toHaveBeenCalledTimes(1);
expect(mockPost).toHaveBeenCalledWith('http://127.0.0.1:5000/register', {
name: 'John',
email: 'john@test.com',
password: 'password123',
isVerified: false
});
});

});
