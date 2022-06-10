function [errorCode, DataBufferLine] = GatheringDataMultipleLinesGet(socketId, IndexPoint, NumberOfLines)
%GatheringDataMultipleLinesGet :  Get multiple data lines from gathering buffer
%
%	[errorCode, DataBufferLine] = GatheringDataMultipleLinesGet(socketId, IndexPoint, NumberOfLines)
%
%	* Input parameters :
%		int32 socketId
%		int32 IndexPoint
%		int32 NumberOfLines
%	* Output parameters :
%		int32 errorCode
%		cstring DataBufferLine


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
DataBufferLine = '';
for i = 1:6554
	DataBufferLine = [DataBufferLine '          '];
end

% lib call
[errorCode, DataBufferLine] = calllib('XPS_Q8_drivers', 'GatheringDataMultipleLinesGet', socketId, IndexPoint, NumberOfLines, DataBufferLine);
