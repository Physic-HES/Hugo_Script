function [errorCode] = PositionerDriverFiltersSet(socketId, PositionerName, KI, NotchFrequency, NotchBandwidth, NotchGain, LowpassFrequency)
%PositionerDriverFiltersSet :  Set driver filters parameters
%
%	[errorCode] = PositionerDriverFiltersSet(socketId, PositionerName, KI, NotchFrequency, NotchBandwidth, NotchGain, LowpassFrequency)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%		double KI
%		double NotchFrequency
%		double NotchBandwidth
%		double NotchGain
%		double LowpassFrequency
%	* Output parameters :
%		int32 errorCode


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% lib call
[errorCode, PositionerName] = calllib('XPS_Q8_drivers', 'PositionerDriverFiltersSet', socketId, PositionerName, KI, NotchFrequency, NotchBandwidth, NotchGain, LowpassFrequency);
