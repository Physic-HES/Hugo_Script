function [errorCode] = GPIODigitalSet(socketId, GPIOName, Mask, DigitalOutputValue)
%GPIODigitalSet :  Set Digital Output for one or few output TTL
%
%	[errorCode] = GPIODigitalSet(socketId, GPIOName, Mask, DigitalOutputValue)
%
%	* Input parameters :
%		int32 socketId
%		cstring GPIOName
%		uint16 Mask
%		uint16 DigitalOutputValue
%	* Output parameters :
%		int32 errorCode


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% lib call
[errorCode, GPIOName] = calllib('XPS_Q8_drivers', 'GPIODigitalSet', socketId, GPIOName, Mask, DigitalOutputValue);
