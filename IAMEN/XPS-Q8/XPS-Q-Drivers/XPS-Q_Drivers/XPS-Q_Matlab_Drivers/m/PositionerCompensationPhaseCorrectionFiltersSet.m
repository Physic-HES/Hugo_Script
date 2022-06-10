function [errorCode] = PositionerCompensationPhaseCorrectionFiltersSet(socketId, PositionerName, PhaseCorrectionFn1, PhaseCorrectionFd1, PhaseCorrectionGain1, PhaseCorrectionFn2, PhaseCorrectionFd2, PhaseCorrectionGain2)
%PositionerCompensationPhaseCorrectionFiltersSet :  Update phase correction filters parameters 
%
%	[errorCode] = PositionerCompensationPhaseCorrectionFiltersSet(socketId, PositionerName, PhaseCorrectionFn1, PhaseCorrectionFd1, PhaseCorrectionGain1, PhaseCorrectionFn2, PhaseCorrectionFd2, PhaseCorrectionGain2)
%
%	* Input parameters :
%		int32 socketId
%		cstring PositionerName
%		double PhaseCorrectionFn1
%		double PhaseCorrectionFd1
%		double PhaseCorrectionGain1
%		double PhaseCorrectionFn2
%		double PhaseCorrectionFd2
%		double PhaseCorrectionGain2
%	* Output parameters :
%		int32 errorCode


% Test that library is loaded
if (~libisloaded('XPS_C8_drivers'))
	disp 'Please load XPS_C8_drivers library before using XPS functions';
	return;
end

% lib call
[errorCode, PositionerName] = calllib('XPS_C8_drivers', 'PositionerCompensationPhaseCorrectionFiltersSet', socketId, PositionerName, PhaseCorrectionFn1, PhaseCorrectionFd1, PhaseCorrectionGain1, PhaseCorrectionFn2, PhaseCorrectionFd2, PhaseCorrectionGain2);
