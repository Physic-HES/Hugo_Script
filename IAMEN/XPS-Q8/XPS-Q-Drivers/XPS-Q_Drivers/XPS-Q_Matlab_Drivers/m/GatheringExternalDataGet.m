function [errorCode, DataBufferLine] = GatheringExternalDataGet(socketId, IndexPoint)
%GatheringExternalDataGet :  Get a data line from external gathering buffer
%
%	[errorCode, DataBufferLine] = GatheringExternalDataGet(socketId, IndexPoint)
%
%	* Input parameters :
%		int32 socketId
%		int32 IndexPoint
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
for i = 1:103
	DataBufferLine = [DataBufferLine '          '];
end

% lib call
[errorCode, DataBufferLine] = calllib('XPS_Q8_drivers', 'GatheringExternalDataGet', socketId, IndexPoint, DataBufferLine);
