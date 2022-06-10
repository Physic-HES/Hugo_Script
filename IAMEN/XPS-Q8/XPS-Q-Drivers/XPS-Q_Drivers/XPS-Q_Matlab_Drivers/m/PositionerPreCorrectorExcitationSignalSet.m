function [errorCode] = PositionerPreCorrectorExcitationSignalSet(socketId, PositionerName, Frequency, Amplitude, Time)
%PositionerPreCorrectorExcitationSignalSet :  Set pre-corrector excitation signal mode
%
%	[errorCode] = PositionerPreCorrectorExcitationSignalSet(socketId, PositionerName, Frequency, Amplitude, Time)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%		double Frequency
%		double Amplitude
%		double Time
%	* Output parameters :
%		int32 errorCode


% Test that library is loaded
if (~libisloaded('XPS_C8_drivers'))
	disp 'Please load XPS_C8_drivers library before using XPS functions';
	return;
end

% lib call
[errorCode, PositionerName] = calllib('XPS_C8_drivers', 'PositionerPreCorrectorExcitationSignalSet', socketId, PositionerName, Frequency, Amplitude, Time);
