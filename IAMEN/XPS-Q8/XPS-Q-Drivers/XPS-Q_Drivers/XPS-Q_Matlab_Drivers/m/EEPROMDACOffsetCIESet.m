function [errorCode] = EEPROMDACOffsetCIESet(socketId, PlugNumber, DAC1Offset, DAC2Offset)
%EEPROMDACOffsetCIESet :  Get raw encoder positions for single axis theta encoder
%
%	[errorCode] = EEPROMDACOffsetCIESet(socketId, PlugNumber, DAC1Offset, DAC2Offset)
%
%	* Input parameters :
%		int32 socketId
%		int32 PlugNumber
%		double DAC1Offset
%		double DAC2Offset
%	* Output parameters :
%		int32 errorCode


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% lib call
[errorCode] = calllib('XPS_Q8_drivers', 'EEPROMDACOffsetCIESet', socketId, PlugNumber, DAC1Offset, DAC2Offset);
