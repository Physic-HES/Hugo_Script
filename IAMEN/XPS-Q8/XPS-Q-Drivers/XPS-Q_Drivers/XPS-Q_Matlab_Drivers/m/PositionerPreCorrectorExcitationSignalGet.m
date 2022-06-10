function [errorCode, Frequency, Amplitude, Time] = PositionerPreCorrectorExcitationSignalGet(socketId, PositionerName)
%PositionerPreCorrectorExcitationSignalGet :  Get pre-corrector excitation signal mode
%
%	[errorCode, Frequency, Amplitude, Time] = PositionerPreCorrectorExcitationSignalGet(socketId, PositionerName)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%	* Output parameters :
%		int32 errorCode
%		doublePtr Frequency
%		doublePtr Amplitude
%		doublePtr Time


% Test that library is loaded
if (~libisloaded('XPS_C8_drivers'))
	disp 'Please load XPS_C8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
Frequency = 0;
Amplitude = 0;
Time = 0;

% lib call
[errorCode, PositionerName, Frequency, Amplitude, Time] = calllib('XPS_C8_drivers', 'PositionerPreCorrectorExcitationSignalGet', socketId, PositionerName, Frequency, Amplitude, Time);
