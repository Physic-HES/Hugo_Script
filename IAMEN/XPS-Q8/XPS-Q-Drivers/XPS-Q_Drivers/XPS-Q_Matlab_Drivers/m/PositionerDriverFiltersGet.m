function [errorCode, KI, NotchFrequency, NotchBandwidth, NotchGain, LowpassFrequency] = PositionerDriverFiltersGet(socketId, PositionerName)
%PositionerDriverFiltersGet :  Get driver filters parameters
%
%	[errorCode, KI, NotchFrequency, NotchBandwidth, NotchGain, LowpassFrequency] = PositionerDriverFiltersGet(socketId, PositionerName)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%	* Output parameters :
%		int32 errorCode
%		doublePtr KI
%		doublePtr NotchFrequency
%		doublePtr NotchBandwidth
%		doublePtr NotchGain
%		doublePtr LowpassFrequency


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
KI = 0;
NotchFrequency = 0;
NotchBandwidth = 0;
NotchGain = 0;
LowpassFrequency = 0;

% lib call
[errorCode, PositionerName, KI, NotchFrequency, NotchBandwidth, NotchGain, LowpassFrequency] = calllib('XPS_Q8_drivers', 'PositionerDriverFiltersGet', socketId, PositionerName, KI, NotchFrequency, NotchBandwidth, NotchGain, LowpassFrequency);
