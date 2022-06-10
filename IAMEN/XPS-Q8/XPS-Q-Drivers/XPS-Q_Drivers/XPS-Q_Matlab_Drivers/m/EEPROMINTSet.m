function [errorCode] = EEPROMINTSet(socketId, CardNumber, ReferenceString)
%EEPROMINTSet :  Get raw encoder positions for single axis theta encoder
%
%	[errorCode] = EEPROMINTSet(socketId, CardNumber, ReferenceString)
%
%	* Input parameters :
%		int32 socketId
%		int32 CardNumber
%		cstring ReferenceString
%	* Output parameters :
%		int32 errorCode


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% lib call
[errorCode, ReferenceString] = calllib('XPS_Q8_drivers', 'EEPROMINTSet', socketId, CardNumber, ReferenceString);
