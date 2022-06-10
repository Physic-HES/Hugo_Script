function [errorCode, DigitalValue] = GPIODigitalGet(socketId, GPIOName)
%GPIODigitalGet :  Read digital output or digital input 
%
%	[errorCode, DigitalValue] = GPIODigitalGet(socketId, GPIOName)
%
%	* Input parameters :
%		int32 socketId
%		cstring GPIOName
%	* Output parameters :
%		int32 errorCode
%		uint16Ptr DigitalValue


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
DigitalValue = 0;

% lib call
[errorCode, GPIOName, DigitalValue] = calllib('XPS_Q8_drivers', 'GPIODigitalGet', socketId, GPIOName, DigitalValue);
