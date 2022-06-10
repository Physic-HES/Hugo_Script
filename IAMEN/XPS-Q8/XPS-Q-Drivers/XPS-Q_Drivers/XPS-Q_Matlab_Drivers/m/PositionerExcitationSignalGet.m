function [errorCode, Mode, Frequency, Amplitude, Time] = PositionerExcitationSignalGet(socketId, PositionerName)
%PositionerExcitationSignalGet :  Get excitation signal mode
%
%	[errorCode, Mode, Frequency, Amplitude, Time] = PositionerExcitationSignalGet(socketId, PositionerName)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%	* Output parameters :
%		int32 errorCode
%		int32Ptr Mode
%		doublePtr Frequency
%		doublePtr Amplitude
%		doublePtr Time


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
Mode = 0;
Frequency = 0;
Amplitude = 0;
Time = 0;

% lib call
[errorCode, PositionerName, Mode, Frequency, Amplitude, Time] = calllib('XPS_Q8_drivers', 'PositionerExcitationSignalGet', socketId, PositionerName, Mode, Frequency, Amplitude, Time);
