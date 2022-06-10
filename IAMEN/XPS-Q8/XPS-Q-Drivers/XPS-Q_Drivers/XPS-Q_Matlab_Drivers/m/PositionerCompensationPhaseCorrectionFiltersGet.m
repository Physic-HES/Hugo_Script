function [errorCode, PhaseCorrectionFn1, PhaseCorrectionFd1, PhaseCorrectionGain1, PhaseCorrectionFn2, PhaseCorrectionFd2, PhaseCorrectionGain2] = PositionerCompensationPhaseCorrectionFiltersGet(socketId, PositionerName)
%PositionerCompensationPhaseCorrectionFiltersGet :  Read phase correction filters parameters 
%
%	[errorCode, PhaseCorrectionFn1, PhaseCorrectionFd1, PhaseCorrectionGain1, PhaseCorrectionFn2, PhaseCorrectionFd2, PhaseCorrectionGain2] = PositionerCompensationPhaseCorrectionFiltersGet(socketId, PositionerName)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%	* Output parameters :
%		int32 errorCode
%		doublePtr PhaseCorrectionFn1
%		doublePtr PhaseCorrectionFd1
%		doublePtr PhaseCorrectionGain1
%		doublePtr PhaseCorrectionFn2
%		doublePtr PhaseCorrectionFd2
%		doublePtr PhaseCorrectionGain2


% Test that library is loaded
if (~libisloaded('XPS_C8_drivers'))
	disp 'Please load XPS_C8_drivers library before using XPS functions';
	return;
end

% Declaration of internal variables
%    (cstring need to be initialized for dll to run fine)
PhaseCorrectionFn1 = 0;
PhaseCorrectionFd1 = 0;
PhaseCorrectionGain1 = 0;
PhaseCorrectionFn2 = 0;
PhaseCorrectionFd2 = 0;
PhaseCorrectionGain2 = 0;

% lib call
[errorCode, PositionerName, PhaseCorrectionFn1, PhaseCorrectionFd1, PhaseCorrectionGain1, PhaseCorrectionFn2, PhaseCorrectionFd2, PhaseCorrectionGain2] = calllib('XPS_C8_drivers', 'PositionerCompensationPhaseCorrectionFiltersGet', socketId, PositionerName, PhaseCorrectionFn1, PhaseCorrectionFd1, PhaseCorrectionGain1, PhaseCorrectionFn2, PhaseCorrectionFd2, PhaseCorrectionGain2);
