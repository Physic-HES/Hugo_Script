function [errorCode, CorrectorType] = PositionerCorrectorTypeGet(socketId, PositionerName)
%PositionerCorrectorTypeGet :  Read corrector type
%
%	[errorCode, CorrectorType] = PositionerCorrectorTypeGet(socketId, PositionerName)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%	* Output parameters :
%		int32 errorCode
%		cstring CorrectorType


% Test that library is loaded
if (~libisloaded('XPS_Q8_drivers'))
	disp 'Please load XPS_Q8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
CorrectorType = '';
for i = 1:103
	CorrectorType = [CorrectorType '          '];
end

% lib call
[errorCode, PositionerName, CorrectorType] = calllib('XPS_Q8_drivers', 'PositionerCorrectorTypeGet', socketId, PositionerName, CorrectorType);
