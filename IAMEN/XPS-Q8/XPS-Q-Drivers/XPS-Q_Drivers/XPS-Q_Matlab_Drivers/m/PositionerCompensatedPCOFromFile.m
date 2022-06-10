function [errorCode] = PositionerCompensatedPCOFromFile(socketId, PositionerName, DataFileName)
%PositionerCompensatedPCOFromFile :  Load file to CIE08 compensated PCO data buffer
%
%	[errorCode] = PositionerCompensatedPCOFromFile(socketId, PositionerName, DataFileName)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%		cstring DataFileName
%	* Output parameters :
%		int32 errorCode


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% lib call
[errorCode, PositionerName, DataFileName] = calllib('XPS_Q8_drivers', 'PositionerCompensatedPCOFromFile', socketId, PositionerName, DataFileName);
